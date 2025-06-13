using Api.Data.DTOS;
using Api.Data.Entities;

namespace Api.Service.Abstracts
{
    public interface IOrganizationService
    {
        Task<List<Organization>> GetOrganizationsAsync();
        Task<Organization> GetOrganizationByIdAsync(int id);
        Task<Organization> GetOrganizationByFacebookidAsync(string id);
        Task<List<Organization>> GetOrganizationsByUseridAsync(string id);
        Task<string> AddOrganizationAsync(Organization organization);
        Task<string> DeleteOrganizationAsync(int id);
        Task<ReportResponse> GetReportAsync(GetReportRequest query);
        Task<ChatResponse> GetChatResponseAsync(GetChatRequest query);
    }
}
