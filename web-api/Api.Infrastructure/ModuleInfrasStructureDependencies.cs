using Api.Infrastructure.Abstracts;
using Api.Infrastructure.InfrastructureBases;
using Api.Infrastructure.Repositories;
using Microsoft.Extensions.DependencyInjection;

namespace Api.Infrastructure
{
    public static class ModuleInfrasStructureDependencies
    {
        public static IServiceCollection AddInfrastructureDependencies(this IServiceCollection services)
        {
            _ = services.AddTransient(typeof(IGenericRepoAsync<>), typeof(GenericRepoAsync<>));
            _ = services.AddTransient<IRefreshTokenRepository, RefreshTokenRepository>();
            _ = services.AddTransient<IOrganizationRepository, OrganizationRespository>();
            _ = services.AddTransient<IReportRepository, ReportRepository>();
            return services;
        }

    }
}
