# Third-party skill sources

These skills are copied here for review and controlled installation. Upstream
instructions do not override the repository's own safety standards.

| Local skill | Upstream source | License | Local status |
| --- | --- | --- | --- |
| `systematic-debugging` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) | MIT | Installed |
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) | MIT | Installed |
| `test-driven-development` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | MIT | Review only |
| `using-git-worktrees` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees) | MIT | Review only |
| `finishing-a-development-branch` | [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) | MIT | Review only |
| `security-best-practices` | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) | Apache-2.0; included upstream license | Installed |
| `security-review` | [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/security-review) | MIT | Review only |
| `code-review-and-quality` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills/code-review-and-quality) | MIT | Installed |
| `azure-devops-safe` | Adapted from [OpenHands/extensions](https://github.com/OpenHands/extensions/tree/main/skills/azure-devops) | MIT; included adaptation license | Review only |

## Deliberately excluded

- The upstream OpenHands Azure DevOps skill was not copied unchanged because
  it recommends putting a PAT in a Git remote URL. `azure-devops-safe` removes
  that behavior and requires credential-free remotes.
- Google Apps Script skills that default to `clasp push --force`, replace the
  global `.clasprc.json`, or switch projects through temporary `.clasp.json`
  files were not imported. The local `oniseb-reliable-coding` skill provides
  the safer script-ID verification rules instead.

Review upstream changes and licenses again before refreshing vendored copies.

