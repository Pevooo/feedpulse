using Api.Core.Features.Authentication.Queries.Models;
using FluentValidation;

namespace Api.Core.Features.Authentication.Queries.Validator
{
    public class ConfirmResetPasswordQueryValidator : AbstractValidator<ConfirmResetPasswordQuery>
    {
        public ConfirmResetPasswordQueryValidator()
        {
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }
        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.Email)
                 .NotEmpty().WithMessage("Email Must not be empty")
                 .NotNull().WithMessage("Email Must not be Null");

            _ = RuleFor(x => x.Code)
                .NotEmpty().WithMessage("Code Must not be Empty")
                .NotNull().WithMessage("Code Must not be Null");
        }

        public void ApplyCustomValidationsRules()
        {
        }

        #endregion
    }
}
