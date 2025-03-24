using Api.Data.Entities;
using Api.Infrastructure.Abstracts;
using Api.Infrastructure.Data;
using Api.Infrastructure.InfrastructureBases;
using Microsoft.EntityFrameworkCore;

namespace Api.Infrastructure.Repositories
{
    internal class ReportRepository : GenericRepoAsync<Reports>, IReportRepository
    {
        #region Fields
        private readonly DbSet<Reports> _reports;
        #endregion
        #region Constructor
        public ReportRepository(ApplicationDbContext context) : base(context)
        {
            _reports = context.Set<Reports>();

        }

        #endregion
        #region HandleFunctions

        #endregion
    }
}
