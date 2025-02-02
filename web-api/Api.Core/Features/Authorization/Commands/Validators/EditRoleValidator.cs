using Api.Core.Features.Authorization.Commands.Models;
using Api.Service.Abstracts;
using FluentValidation;

namespace Api.Core.Features.Authorization.Commands.Validators
{
    public class EditRoleValidator : AbstractValidator<EditRoleCommand>
    {
        #region Fields
        IAuthorizationService _authorizationService;
        #endregion
        #region Constructors
        public EditRoleValidator(IAuthorizationService authorizationService)
        {
            _authorizationService = authorizationService;
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }
        #endregion
        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.Id)
                 .NotEmpty().WithMessage("Id must not be empty")
                 .NotNull().WithMessage("Id must not be Null");

            _ = RuleFor(x => x.Name)
                 .NotEmpty().WithMessage("Name must not be Empty")
                 .NotNull().WithMessage("Name must not be Null");
        }

        public void ApplyCustomValidationsRules()
        {
            _ = RuleFor(x => x.Name)
                .MustAsync(async (Key, CancellationToken) => !await _authorizationService.IsRoleExistByName(Key))
                .WithMessage("The Role Exist Before");

        }

        #endregion
    }
}
