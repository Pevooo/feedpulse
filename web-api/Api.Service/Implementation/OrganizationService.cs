using Api.Data.Entities;
using Api.Infrastructure.Abstracts;
using Api.Service.Abstracts;
using Microsoft.EntityFrameworkCore;

namespace Api.Service.Implementation
{
    public class OrganizationService : IOrganizationService
    {
        #region Fields
        IOrganizationRepository _organizationRepository;
        #endregion
        #region Constructor
        public OrganizationService(IOrganizationRepository organizationRepository)
        {
            _organizationRepository = organizationRepository;
        }

        public Task<string> AddOrganizationAsync(Organization organization)
        {
            // check on accesstoken 
            // get long lived token
            // send the description and accesstoken to ai api 
            // add the organization
            throw new NotImplementedException();

        }

        #endregion
        #region HandleFunctions
        public async Task<Organization> GetOrganizationByFacebookidAsync(string id)
        {
            return await _organizationRepository.GetTableNoTracking().Where(x => x.FacebookId == id).SingleOrDefaultAsync();
        }

        public async Task<Organization> GetOrganizationByIdAsync(int id)
        {
            return await _organizationRepository.GetByIdAsync(id);
        }

        public async Task<List<Organization>> GetOrganizationsAsync()
        {
            return await _organizationRepository.GetTableNoTracking().ToListAsync();
        }

        public async Task<List<Organization>> GetOrganizationsByUseridAsync(string id)
        {
            return await _organizationRepository.GetTableNoTracking().Where(x => x.UserId == id).ToListAsync();
        }
        #endregion
    }
}
