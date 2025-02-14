using Api.Core.Features.Authentication.Command.Models;
using FluentValidation;

namespace Api.Core.Features.Authentication.Command.Validators
{
    public class SignInCommandValidator : AbstractValidator<SignInCommand>
    {
        public SignInCommandValidator()
        {
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }

        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.UserName)
                 .NotEmpty().WithMessage("UserName must not be empty")
                 .NotNull().WithMessage("UserName must not be NULL");

            _ = RuleFor(x => x.Password)
                .NotEmpty().WithMessage("Password must not be empty")
                .NotNull().WithMessage("Password must not be Null");
        }

        public void ApplyCustomValidationsRules()
        {
        }

        #endregion
    }
}
