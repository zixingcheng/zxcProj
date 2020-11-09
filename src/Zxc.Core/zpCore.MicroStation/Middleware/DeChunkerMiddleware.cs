using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using System;
using System.Net;
using System.Threading.Tasks;

public class DeChunkerMiddleware
{
    private readonly RequestDelegate _next;

    public DeChunkerMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var originalBodyStream = context.Response.Body;
        using (var responseBody = new System.IO.MemoryStream())
        {
            context.Response.Body = responseBody;
            long length = 0;
            context.Response.OnStarting(() =>
            {
                context.Response.Headers.ContentLength = length;
                return Task.CompletedTask;
            });
            await _next(context);
            //if you want to read the body, uncomment these lines.
            //context.Response.Body.Seek(0, SeekOrigin.Begin);
            //var body = await new StreamReader(context.Response.Body).ReadToEndAsync();
            length = context.Response.Body.Length;
            context.Response.Body.Seek(0, System.IO.SeekOrigin.Begin);
            await responseBody.CopyToAsync(originalBodyStream);
        }
    }
}