using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.FileProviders;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using zpCore.Common;
using zpCore.GIS.API.Models;
using zpCore.GIS.API.Models.JobTrigger;

namespace zpCore.GIS.API
{
    public class Startup
    {
        readonly string MyAllowSpecificOrigins = "_myAllowSpecificOrigins";
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(options =>
            {
                options.AddPolicy(name: MyAllowSpecificOrigins,
                                  builder =>
                                  {
                                      builder.WithOrigins("http://example.com",
                                                          "http://www.contoso.com")
                                        .AllowAnyHeader()
                                        .AllowAnyOrigin()
                                        .AllowAnyMethod();
                                  });
            });
            services.AddControllers();

            // ������Ϣ
            services.Configure<FileSetOptions >(Configuration.GetSection("FileSetOptions"));
            services.Configure<GisSetOptions>(Configuration.GetSection("GisSetOptions"));

            // ��Ӷ�ʱ����
            //services.AddHostedService<WzDatas_DistributionTaskJobTrigger>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseMiddleware<DeChunkerMiddleware>();

            app.UseHttpsRedirection();
            app.UseRouting();
            app.UseAuthorization();
            app.UseErrorHandling();


            app.UseCors(MyAllowSpecificOrigins);
            app.UseStaticFiles(new StaticFileOptions()
            {
                ServeUnknownFileTypes = true,
                FileProvider = new PhysicalFileProvider(
                Path.Combine(Directory.GetCurrentDirectory(), "wwwroot")),  //wwwroot�൱����ʵĿ¼
                RequestPath = new PathString("/src")                        //src�൱�ڱ�����Ϊ�˰�ȫ
            });

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });

            // ��ȡ�����ļ�������
            MyServiceProvider.ServiceProvider = app.ApplicationServices;
        }
    }
}
