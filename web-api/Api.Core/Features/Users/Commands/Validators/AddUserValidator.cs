using Api.Core.Features.Users.Commands.Models;
using FluentValidation;

namespace Api.Core.Features.Users.Commands.Validators
{
    public class AddUserValidator : AbstractValidator<AddUserCommand>
    {
        #region fields
        #endregion
        #region constructor
        public AddUserValidator()
        {
            ApplyValidationsRules();
            ApplyCustomValidationsRules();
        }
        #endregion
        #region handlefunctions
        public void ApplyValidationsRules()
        {
            _ = RuleFor(x => x.FullName).
                NotEmpty().WithMessage("Name Must ")
                .NotNull().WithMessage("Name Must Be Not Null")
                .MaximumLength(200).WithMessage("Max Length is 200");

            _ = RuleFor(x => x.UserName)
                .NotEmpty().WithMessage("{PropertyName} Must Not Be Empty")
                .NotNull().WithMessage("{PropertyName} Must Be Null")
                .MaximumLength(100).WithMessage("{PropertyName} Length is 100");

            _ = RuleFor(x => x.Email)
            .NotEmpty().WithMessage("{PropertyName} Must Not Be Empty")
            .NotNull().WithMessage("{PropertyName} Must Be Null");

            _ = RuleFor(x => x.Password)
            .NotEmpty().WithMessage("{PropertyName} Must Not Be Empty")
            .NotNull().WithMessage("{PropertyName} Must Be Null");

            _ = RuleFor(x => x.ConfirmPassword)
           .NotEmpty().WithMessage("{PropertyName} Must Not Be Empty")
           .NotNull().WithMessage("{PropertyName} Must Be Null")
           .Equal(c => c.Password).WithMessage("The Confirm Password dosent match the password");
            _ = RuleFor(x => x.Description)
          .NotEmpty().WithMessage("{PropertyName} Must Not Be Empty")
          .NotNull().WithMessage("{PropertyName} Must Be Null");



        }
        public void ApplyCustomValidationsRules()// el false hwa el bedrb error
        {

        }
        #endregion
    }
}
