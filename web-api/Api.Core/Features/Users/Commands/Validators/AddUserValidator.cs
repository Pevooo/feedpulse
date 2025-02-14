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

            _ = RuleFor(x => x.Photo)
            .NotEmpty().WithMessage("Base64Data is required.")
            .MaximumLength(10485760).WithMessage("Base64Data cannot exceed 10 MB.")
            .Must(BeAValidBase64String).WithMessage("Invalid Base64 string.");



        }
        public void ApplyCustomValidationsRules()// el false hwa el bedrb error
        {

        }
        private bool BeAValidBase64String(string base64Data)
        {
            if (string.IsNullOrEmpty(base64Data))
                return false;

            try
            {
                // Attempt to convert the Base64 string to a byte array
                _ = Convert.FromBase64String(base64Data);
                return true;
            }
            catch
            {
                return false;
            }
        }
        #endregion
    }
}
