using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

using Newtonsoft.Json;
using zpCore.MicroStation.JobTrigger;
using zpCore.MicroStation.Models;
using zpCore.MicroStation.Common;
using Microsoft.Extensions.FileProviders;
using System.IO;
using Microsoft.AspNetCore.Http;

namespace zpCore.MicroStation
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
            services.AddControllers();      //.AddNewtonsoftJson();

            // EF����
            common.coon = Configuration["ConnectionSetting:coon_MicroStation"];
            services.AddDbContext<db_MicroStationContext>(optionsBuilder =>
            {
                optionsBuilder.UseMySQL(common.coon);
            });
            services.AddDbContext<dg_dbContext>(optionsBuilder =>
            {
                string coon = Configuration["ConnectionSetting:coon_KPR"];
                optionsBuilder.UseMySQL(coon);
            });

            // ͼƬAPI
            services.Configure<PictureOptions>(Configuration.GetSection("PictureOptions"));
            common.ftpDir = Configuration["PictureOptions:ImageBaseUrl"];

            // ��Ӷ�ʱ����
            services.AddHostedService<FtpAlarmJobTrigger>();
            services.AddHostedService<FtpTaskJobTrigger>();
            services.AddHostedService<FtpUserJobTrigger>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseMiddleware<DeChunkerMiddleware>();

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

                //��Ч����ͣʹ��
                //endpoints.MapControllerRoute(
                //    name: "default",
                //    pattern: "{controller=Home}/{action=Index}/{id?}");

                ////���������󣬴˹��򲻻��Զ�����������
                //endpoints.MapAreaControllerRoute(
                //       name: "areas", "areas",
                //       pattern: "{area:exists}/{controller=Home}/{action=Index}/{id?}");
            });
        }
    }
}
