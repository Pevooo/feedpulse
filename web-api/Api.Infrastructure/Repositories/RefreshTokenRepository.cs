using Api.Data.Entities.Identity;
using Api.Infrastructure.Abstracts;
using Api.Infrastructure.Data;
using Api.Infrastructure.InfrastructureBases;
using Microsoft.EntityFrameworkCore;

namespace Api.Infrastructure.Repositories
{
    public class RefreshTokenRepository : GenericRepoAsync<UserRefershToken>, IRefreshTokenRepository
    {
        #region Fields
        private readonly DbSet<UserRefershToken> _userRefreshToken;
        #endregion
        #region Constructor
        public RefreshTokenRepository(ApplicationDbContext context) : base(context)
        {
            _userRefreshToken = context.Set<UserRefershToken>();

        }

        #endregion
        #region HandleFunctions

        #endregion
    }
}
