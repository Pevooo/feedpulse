using Api.Core.Features.Authentication.Queries.Models;
using FluentValidation;

namespace Api.Core.Features.Authentication.Queries.Validator
{
    public class ConfirmEmailQueryValidator : AbstractValidator<ConfirmEmailQuery>
    {
        #region Constructors
        public ConfirmEmailQueryValidator()
        {
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }
        #endregion

        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.UserId)
                 .NotEmpty().WithMessage("UserId Must not be empty")
                 .NotNull().WithMessage("UserId Must not be Null");

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
