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
using zpCore.MicroStation.Models;

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

            // EF配置
            services.AddDbContext<db_MicroStationContext>(optionsBuilder =>
            {
                string coon = Configuration["ConnectionSetting:coon_MicroStation"];
                optionsBuilder.UseMySQL(coon);
            });
            services.AddDbContext<dg_dbContext>(optionsBuilder =>
            {
                string coon = Configuration["ConnectionSetting:coon_KPR"];
                optionsBuilder.UseMySQL(coon);
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseRouting();
            app.UseAuthorization();

            app.UseErrorHandling();

            app.UseCors(MyAllowSpecificOrigins);

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();

                //无效，暂停使用
                //endpoints.MapControllerRoute(
                //    name: "default",
                //    pattern: "{controller=Home}/{action=Index}/{id?}");

                ////添加了区域后，此规则不会自动创建！！！
                //endpoints.MapAreaControllerRoute(
                //       name: "areas", "areas",
                //       pattern: "{area:exists}/{controller=Home}/{action=Index}/{id?}");
            });
        }
    }
}
