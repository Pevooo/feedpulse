using Api.Core.Features.Authentication.Command.Models;
using FluentValidation;

namespace Api.Core.Features.Authentication.Command.Validators
{
    public class SendResetPasswordCommandValidator : AbstractValidator<SendResetPasswordCommand>
    {
        public SendResetPasswordCommandValidator()
        {
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }
        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.Email)
                 .NotEmpty().WithMessage("Email must be not empty")
                 .NotNull().WithMessage("Email must be not null");


        }

        public void ApplyCustomValidationsRules()
        {
        }

        #endregion
    }
}
