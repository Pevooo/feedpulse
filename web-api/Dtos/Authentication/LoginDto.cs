using System.ComponentModel.DataAnnotations;

namespace web_api.Dtos.Authentication
{
    public class LoginDto
    {
        [EmailAddress]
        public string Email { get; set; }
        public string Password { get; set; }
    }
}
