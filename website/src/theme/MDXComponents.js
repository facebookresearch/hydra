// Import the original mapper
import MDXComponents from '@theme-original/MDXComponents';
import GithubLink from '@site/src/components/GithubLink';

export default {
  // Re-use the default mapping
  ...MDXComponents,
  // Map the "<Highlight>" tag to our Highlight component
  // `Highlight` will receive all props that were passed to `<Highlight>` in MDX
  GithubLink,
};
