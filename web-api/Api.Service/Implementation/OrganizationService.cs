using Api.Data.Entities;
using Api.Data.Helpers;
using Api.Infrastructure.Abstracts;
using Api.Infrastructure.Data;
using Api.Service.Abstracts;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using System.Text;
using System.Text.Json;

namespace Api.Service.Implementation
{
    public class OrganizationService : IOrganizationService
    {
        #region Fields
        private readonly IOrganizationRepository _organizationRepository;
        private readonly FacebookSettings _facebookSettings;
        private readonly HttpClient _httpClient;
        private readonly IFacebookService _facebookService;
        private readonly ApplicationDbContext _applicationDbContext;

        #endregion
        #region Constructor
        public OrganizationService(IOrganizationRepository organizationRepository, ApplicationDbContext applicationDbContext,
            HttpClient httpClient, IOptions<FacebookSettings> options, IFacebookService facebookService)
        {
            _organizationRepository = organizationRepository;
            _facebookSettings = options.Value;
            _httpClient = httpClient;
            _facebookService = facebookService;
            _applicationDbContext = applicationDbContext;
        }

        public async Task<string> AddOrganizationAsync(Organization organization)
        {

            var trans = _applicationDbContext.Database.BeginTransaction();
            try
            {
                // get long lived token
                var longlivedtoken = await _facebookService.ExchangeForLongLivedPageToken(organization.PageAccessToken);
                organization.PageAccessToken = longlivedtoken;

                // send the facebookpageid ,description and accesstoken to ai api 
                var url = "https://localhost:5000/register_token";

                var requestBody = new
                {
                    page_id = organization.FacebookId,
                    access_token = longlivedtoken,
                    platform = "Facebook"
                };

                var jsonContent = new StringContent(
                    JsonSerializer.Serialize(requestBody),
                    Encoding.UTF8,
                    "application/json"
                );

                var response = await _httpClient.PostAsync(url, jsonContent);

                if (!response.IsSuccessStatusCode)
                {
                    throw new Exception($"Error: {response.StatusCode} - {await response.Content.ReadAsStringAsync()}");
                }
                // add the organization
                _ = _applicationDbContext.Organizations.Add(organization);

                trans.Commit();
            }
            catch (Exception ex)
            {
                trans.Rollback();
                return ex.Message;
            }
            return "Success";


        }

        public async Task<string> DeleteOrganizationAsync(int id)
        {
            var orgnaizaton = await _organizationRepository.GetByIdAsync(id);
            if (orgnaizaton == null) { return "NotFound"; }
            await _organizationRepository.DeleteAsync(orgnaizaton);
            return "Success";
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
