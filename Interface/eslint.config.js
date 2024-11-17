// eslint.config.js
module.exports = {
  overrides: [
    {
      files: ['*.ts', '*.tsx'], // Lint all TypeScript and TypeScript JSX files
      parser: '@typescript-eslint/parser', // Specify the TypeScript parser
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
      },
      plugins: ['@typescript-eslint'],
      extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:@angular-eslint/recommended', // Recommended rules for Angular
      ],
      rules: {
        'no-console': 'warn',  // Example rule: warn on console statements
        '@typescript-eslint/no-explicit-any': 'warn'  // Example TypeScript-specific rule
      }
    }
  ]
};
