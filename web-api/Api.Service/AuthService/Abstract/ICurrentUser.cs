using Api.Data.Entities.Identity;

namespace Api.Service.AuthService.Abstract
{
    public interface ICurrentUser
    {
        public Task<Organization> GetUserAsync();
        public int GetUserId();
        public Task<List<string>> GetCurrentUserRolesAsync();
    }
}
