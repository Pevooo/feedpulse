using Api.Core;
using Api.Data.Entities.Identity;
using Api.Infrastructure;
using Api.Infrastructure.Data;
using Api.Infrastructure.Seeder;
using Api.Service;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Infrastructure;
using Microsoft.AspNetCore.Mvc.Routing;
using Microsoft.EntityFrameworkCore;
using School.Core.MiddleWare;

namespace web_api
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            _ = builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            _ = builder.Services.AddEndpointsApiExplorer();
            _ = builder.Services.AddSwaggerGen();
            _ = builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));
            _ = builder.Services.ServiceRegisterationmethod(builder.Configuration);
            #region AddDependices
            _ = builder.Services.AddServiceDependencies().
            AddInfrastructureDependencies().
            AddCoreDependencies();
            #endregion
            #region AllowCORS
            var CORS = "_cors";
            _ = builder.Services.AddCors(options =>
            {
                options.AddPolicy(name: CORS,
                                  policy =>
                                  {
                                      _ = policy.AllowAnyHeader();
                                      _ = policy.AllowAnyMethod();
                                      _ = policy.AllowAnyOrigin();
                                  });
            });
            _ = builder.Services.AddSingleton<IActionContextAccessor, ActionContextAccessor>();
            _ = builder.Services.AddTransient<IUrlHelper>(x =>
            {
                var actionContext = x.GetRequiredService<IActionContextAccessor>().ActionContext;
                var factory = x.GetRequiredService<IUrlHelperFactory>();
                return factory.GetUrlHelper(actionContext);
            });
            #endregion
            var app = builder.Build();
            #region Seeder

            using (var scope = app.Services.CreateScope())
            {
                var userManager = scope.ServiceProvider.GetRequiredService<UserManager<Organization>>();
                var roleManager = scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>();
                await RoleSeeder.SeedAsync(roleManager);
                await UserSeeder.SeedAsync(userManager);
            }
            #endregion

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                _ = app.UseSwagger();
                _ = app.UseSwaggerUI();
            }
            _ = app.UseMiddleware<ErrorHandlerMiddleware>();
            _ = app.UseHttpsRedirection();
            _ = app.UseCors(CORS);
            _ = app.UseAuthorization();


            _ = app.MapControllers();

            app.Run();
        }
    }
}
