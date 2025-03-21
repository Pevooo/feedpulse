using Api.Data.Entities;
using Api.Infrastructure.Abstracts;
using Api.Infrastructure.Data;
using Api.Infrastructure.InfrastructureBases;
using Microsoft.EntityFrameworkCore;

namespace Api.Infrastructure.Repositories
{
    public class OrganizationRespository : GenericRepoAsync<Organization>, IOrganizationRepository
    {
        #region Fields
        private readonly DbSet<Organization> _Organization;
        #endregion
        #region Constructor
        public OrganizationRespository(ApplicationDbContext context) : base(context)
        {
            _Organization = context.Set<Organization>();

        }

        #endregion
        #region HandleFunctions

        #endregion
    }
}
