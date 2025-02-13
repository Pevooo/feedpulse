using Api.Data.DTOS;
using Api.Data.Entities.Identity;
using Api.Data.Requests;
using Microsoft.AspNetCore.Identity;

namespace Api.Service.Abstracts
{
    public interface IAuthorizationService
    {
        public Task<string> AddRoleAsync(string roleName);
        public Task<string> EditRoleAsync(EditRoleRequest request);

        public Task<bool> IsRoleExistByName(string roleName);
        public Task<string> DeleteRoleAsync(int RoleId);
        public Task<List<IdentityRole>> GetRolesList();
        public Task<IdentityRole> GetRoleById(string id);
        public Task<ManageUserRolesResponse> ManageUserRolesData(Organization user);
        public Task<string> UpdateUserRole(UpdateUserRolesRequest request);
        public Task<string> UpdateUserClaims(ManageUserClaimsRequest request);
        //public Task<ManageUserClaimsResponse> ManageUserClaimData(Organization User);
    }
}
