using Api.Data.Entities.Identity;
using Api.Infrastructure.InfrastructureBases;

namespace Api.Infrastructure.Abstracts
{
    public interface IRefreshTokenRepository : IGenericRepoAsync<UserRefershToken>
    {
    }
}
