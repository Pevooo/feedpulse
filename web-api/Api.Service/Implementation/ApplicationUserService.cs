using Api.Data.Entities.Identity;
using Api.Infrastructure.Data;
using Api.Service.Abstracts;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace Api.Service.Implementation
{
    public class ApplicationUserService : IApplicationUserService
    {
        #region Fields
        private readonly UserManager<Organization> _userManager;
        private readonly IEmailService _emailService;
        private readonly IHttpContextAccessor _httpContextAccessor;
        private readonly ApplicationDbContext _dbcontext;
        private readonly IUrlHelper _urlHelper;
        #endregion
        #region Constructor
        public ApplicationUserService(UserManager<Organization> userManager,
                                     IHttpContextAccessor httpContextAccessor,
                                     IEmailService emailsService,
                                     ApplicationDbContext applicationDBContext,
                                     IUrlHelper urlHelper)
        {
            _userManager = userManager;
            _httpContextAccessor = httpContextAccessor;
            _emailService = emailsService;
            _dbcontext = applicationDBContext;
            _urlHelper = urlHelper;
        }


        #endregion
        #region HandleFunctions
        public async Task<string> AddUser(Organization user, string password)
        {
            var trans = _dbcontext.Database.BeginTransaction();
            try
            {
                //if Email is Exist
                var existUser = await _userManager.FindByEmailAsync(user.Email);
                //email is Exist
                if (existUser != null) return "EmailIsExist";

                var userByUserName = await _userManager.FindByNameAsync(user.UserName);
                //username is Exist
                if (userByUserName != null) return "UserNameIsExist";
                //Create
                var createResult = await _userManager.CreateAsync(user, password);
                //Failed
                if (!createResult.Succeeded)
                    return string.Join(",", createResult.Errors.Select(x => x.Description).ToList());

                _ = await _userManager.AddToRoleAsync(user, "User");

                //Send Confirm Email
                var code = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                var resquestAccessor = _httpContextAccessor.HttpContext.Request;
                var returnUrl = resquestAccessor.Scheme + "://" + resquestAccessor.Host + _urlHelper.Action("ConfirmEmail", "Authentication", new { userId = user.Id, code = code });
                var message = $"To Confirm Email Click Link: <a href='{returnUrl}'>Link Of Confirmation</a>";
                //$"/Api/V1/Authentication/ConfirmEmail?userId={user.Id}&code={code}";
                //message or body
                _ = await _emailService.SendEmail(user.Email, message, "ConFirm Email");

                trans.Commit();
                return "Success";
            }
            catch (Exception ex)
            {

                trans.Rollback();
                return "Failed";
            }
        }
        #endregion
    }
}
