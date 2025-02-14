using Api.Data.Entities.Identity;

namespace Api.Service.Abstracts
{
    public interface IApplicationUserService
    {
        public Task<string> AddUser(Organization user, string password);
    }
}
