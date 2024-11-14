using web_api.Services.Interfaces;

namespace web_api.UnitOfWork
{
    public interface IUnitOfWork
    {
        ICategoryService CategoryService { get; }
        int Complete();
    }
}
