# NewsFlow Frontend

This project is built with Svelte, TypeScript, Vite, and TailwindCSS. It also includes configuration for ESLint, Prettier, and Vitest for testing.

## Table of Contents

- [Installation](#installation)
- [Scripts](#scripts)
- [Configuration](#configuration)
- [Folder Structure](#folder-structure)
- [Linting and Formatting](#linting-and-formatting)
- [Testing](#testing)

## Installation

To get started, clone the repository and install the dependencies using `pnpm`:

```bash
git clone <repository-url>
cd <repository-directory>
pnpm install
```

## Scripts

The following scripts are available in this project:

- `dev`: Start the development server.
- `build`: Build the project for production.
- `preview`: Preview the production build.
- `lint`: Lint the codebase using ESLint.
- `format`: Format the codebase using Prettier.
- `test`: Run the tests using Vitest.

You can run these scripts using `pnpm`:

```bash
pnpm dev
pnpm build
pnpm preview
pnpm lint
pnpm format
pnpm test
```

## Configuration

### ESLint

The ESLint configuration is defined in `eslint.config.mjs`. It includes support for Svelte, TypeScript, and Prettier.

### TailwindCSS

The TailwindCSS configuration is defined in `tailwind.config.js`. The `content` array specifies the files TailwindCSS should scan for class names.

### Vite

The Vite configuration is defined in `vite.config.js`. It includes the Svelte plugin with preprocessing.

### Svelte

The Svelte configuration is defined in `svelte.config.ts`. It uses `svelte-preprocess` for preprocessing.

### Vitest

The Vitest configuration is defined in `vitest.config.ts`. It includes the Svelte plugin and settings for running tests with JSDOM.

## Folder Structure

The project has the following structure:

- `src/`: Contains the source code of the project.
  - `components/`: Contains Svelte components.
  - `stores/`: Contains Svelte stores.
  - `styles/`: Contains global styles.
  - `tests/`: Contains test files.
  - `App.svelte`: Main Svelte component.
  - `main.ts`: Entry point of the application.
  - `setupTests.ts`: Test setup file.
- `public/`: Contains public assets and the `index.html` file.
- `.eslintrc.js`: ESLint configuration file.
- `tailwind.config.js`: TailwindCSS configuration file.
- `vite.config.js`: Vite configuration file.
- `svelte.config.ts`: Svelte configuration file.
- `vitest.config.ts`: Vitest configuration file.
- `pnpm-lock.yaml`: Lockfile for pnpm.
- `README.md`: This file.

## Linting and Formatting

This project uses ESLint for linting and Prettier for code formatting. You can lint and format the codebase using the following commands:

```bash
pnpm lint
pnpm format
```

## Testing

This project uses Vitest for testing. Test files are located in the `src/tests/` directory and should have a `.test.ts` extension. You can run the tests using the following command:

```bash
pnpm test
```

## License

This project is licensed under the AGPL-3.0-only License. See the [LICENSE](LICENSE) file for details.
