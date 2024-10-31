using System.ComponentModel.DataAnnotations;

namespace web_api.Dtos.Authentication
{
    public class RegisterDto
    {
        [Required, MaxLength(60)]
        public string OrgnaizationName { get; set; } = string.Empty;
        [Required, MaxLength(50)]
        public string UserName { get; set; } = string.Empty;
        [EmailAddress]
        public string Email { get; set; } = string.Empty;
        [Required]
        public string Password { get; set; } = string.Empty;
        [Required]
        public string PhoneNumber { get; set; } = string.Empty;
        [Required]
        public string Country { get; set; } = string.Empty;
        [Required]
        public string City { get; set; } = string.Empty;
        [Required]
        public string Describtion { get; set; } = string.Empty;
    }
}
