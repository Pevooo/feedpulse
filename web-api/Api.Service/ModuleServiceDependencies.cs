using Api.Service.Abstracts;
using Api.Service.AuthService.Abstract;
using Api.Service.AuthService.Implementation;
using Api.Service.Implementation;
using Microsoft.Extensions.DependencyInjection;

namespace Api.Service
{
    public static class ModuleServiceDependencies
    {

        public static IServiceCollection AddServiceDependencies(this IServiceCollection services)
        {
            _ = services.AddTransient<IEmailService, EmailService>();
            _ = services.AddTransient<ICurrentUser, CurrentUserService>();
            _ = services.AddTransient<IAuthenticationService, AuthenticationService>();
            _ = services.AddTransient<IAuthorizationService, AuthorizationService>();
            _ = services.AddTransient<IApplicationUserService, ApplicationUserService>();
            _ = services.AddTransient<IFileService, FileService>();
            _ = services.AddTransient<IFacebookService, FacebookService>();
            return services;
        }
    }
}
