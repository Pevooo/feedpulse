using Api.Data.Entities.Identity;
using Microsoft.AspNetCore.Http;

namespace Api.Service.Abstracts
{
    public interface IApplicationUserService
    {
        public Task<string> AddUser(AppUser user, string password, IFormFile photo);
    }
}
