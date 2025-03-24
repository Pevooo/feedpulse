using Api.Core.Features.Organizations.Commands.Models;
using FluentValidation;

namespace Api.Core.Features.Organizations.Commands.Validators
{
    public class AddOrganizationCommandValidator : AbstractValidator<AddOrganizationCommand>
    {
        public AddOrganizationCommandValidator()
        {

        }
        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.Name)
                 .NotEmpty().WithMessage("Organization Name must not be empty")
                 .NotNull().WithMessage("Organization Name must not be Null");
            _ = RuleFor(x => x.Description)
             .NotEmpty().WithMessage("Description Name must not be empty")
             .NotNull().WithMessage("Description Name must not be Null");
            _ = RuleFor(x => x.UserId)
             .NotEmpty().WithMessage("UserId Name must not be empty")
             .NotNull().WithMessage("UserId Name must not be Null");
            _ = RuleFor(x => x.PageAccessToken)
             .NotEmpty().WithMessage("PageAccessToken Name must not be empty")
             .NotNull().WithMessage("PageAccessToken Name must not be Null");
            _ = RuleFor(x => x.FacebookId)
             .NotEmpty().WithMessage("FacebookId Name must not be empty")
             .NotNull().WithMessage("FacebookId Name must not be Null");
        }

        public void ApplyCustomValidationsRules()
        {

        }
    }
    #endregion
}
