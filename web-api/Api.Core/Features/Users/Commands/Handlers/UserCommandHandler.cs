using Api.Core.Bases;
using Api.Core.Features.Users.Commands.Models;
using Api.Data.Entities.Identity;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace Api.Core.Features.Users.Commands.Handlers
{
    public class UserCommandHandler : ResponseHandler,
                                                IRequestHandler<AddUserCommand, Response<string>>,
                                                IRequestHandler<DeleteUserCommand, Response<string>>,
                                                IRequestHandler<EditUserCommand, Response<string>>,
                                                IRequestHandler<ChangeUserPasswordCommand, Response<string>>
    {
        #region Fields
        private readonly IMapper _mapper;
        private readonly UserManager<AppUser> _userManager;
        private readonly IApplicationUserService _applicationUserService;
        #endregion
        #region Constructors
        public UserCommandHandler(IMapper mapper, UserManager<AppUser> userManager, IApplicationUserService applicationService)
        {
            _mapper = mapper;
            _userManager = userManager;
            _applicationUserService = applicationService;
        }
        #endregion
        #region HandlesFunctions
        public async Task<Response<string>> Handle(AddUserCommand request, CancellationToken cancellationToken)
        {
            var identityUser = new AppUser()
            {
                FullName = request.FullName,
                Email = request.Email,
                Address = request.Address,
                Country = request.Country,
                UserName = request.UserName,
                PhoneNumber = request.PhoneNumber,

            };
            var result = await _applicationUserService.AddUser(identityUser, request.Password, request.Photo);
            switch (result)
            {
                case "EmailIsExist":
                    return BadRequest<string>(result);
                case "UserNameIsExist": return BadRequest<string>(result);
                case "ErrorInCreateUser": return BadRequest<string>(result);
                case "Failed": return BadRequest<string>(result);
                case "Success": return Success<string>("");
                default: return BadRequest<string>(result);
            }

        }
        public async Task<Response<string>> Handle(DeleteUserCommand request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByIdAsync(request.Id);
            if (user == null) { return NotFound<string>("User is not Exist"); }
            var result = await _userManager.DeleteAsync(user);
            if (!result.Succeeded) return BadRequest<string>("Something Went Wrong");
            return Success("");
        }
        public async Task<Response<string>> Handle(EditUserCommand request, CancellationToken cancellationToken)
        {
            var olduser = await _userManager.FindByIdAsync(request.Id);
            if (olduser == null) { return NotFound<string>("Not Exist"); }
            var newUser = _mapper.Map(request, olduser);
            //if username is Exist
            var userByUserName = await _userManager.Users.FirstOrDefaultAsync(x => x.UserName == newUser.UserName && x.Id != newUser.Id);
            //username is Exist
            if (userByUserName != null) return BadRequest<string>("UserName is Exist Before!");

            var result = await _userManager.UpdateAsync(newUser);
            if (!result.Succeeded)
            {
                return BadRequest<string>("Someting went wrong");
            }
            return Success("");
        }
        public async Task<Response<string>> Handle(ChangeUserPasswordCommand request, CancellationToken cancellationToken)
        {
            //get user
            //check if user is exist
            var user = await _userManager.FindByIdAsync(request.id.ToString());
            //if Not Exist notfound
            if (user == null) return NotFound<string>();

            var result = await _userManager.ChangePasswordAsync(user, request.CurrentPassword, request.NewPassword);
            if (!result.Succeeded) return BadRequest<string>("something went wrong!");
            return Success("Done");

        }
        #endregion
    }
}
