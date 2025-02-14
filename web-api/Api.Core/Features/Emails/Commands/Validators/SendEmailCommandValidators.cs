using Api.Core.Features.Emails.Commands.Models;
using FluentValidation;

namespace Api.Core.Features.Emails.Commands.Validators
{
    public class SendEmailCommandValidators : AbstractValidator<SendEmailCommand>
    {
        #region Constructors
        public SendEmailCommandValidators()
        {
            ApplyValidationsRules();
        }
        #endregion
        #region Actions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.Email)
                 .NotEmpty().WithMessage("Email must not be empty")
                 .NotNull().WithMessage("Email must not be null");

            _ = RuleFor(x => x.Message)
                 .NotEmpty().WithMessage("Message must not be empty")
                 .NotNull().WithMessage("Message must not be null");
        }
        #endregion
    }
}
