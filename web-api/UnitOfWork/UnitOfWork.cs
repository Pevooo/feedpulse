using web_api.Data;
using web_api.Services.Interfaces;
using web_api.Services.Repos;

namespace web_api.UnitOfWork
{
    public class UnitOfWork : IUnitOfWork
    {
        #region fields
        private readonly ApplicationDbContext _context;

        public ICategoryService CategoryService { get; private set; }



        #endregion
        #region Constructor
        public UnitOfWork(ApplicationDbContext context)
        {
            _context = context;

            CategoryService = new CategoryService(context);

        }
        #endregion
        #region HandleFunctions
        public int Complete()
        {
            return _context.SaveChanges();
        }

        public void Dispose()
        {
            _context.Dispose();
        }
        #endregion
    }
}
