name: ✨ Feature Request
description: Propose a new feature, improvement, or roadmap suggestion
title: "[FEATURE] "
labels: ["enhancement"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        We are always looking to improve HydrateMe! Please describe your proposed enhancement below.
  - type: textarea
    id: problem
    attributes:
      label: Is your feature request related to a problem?
      description: A clear and concise description of what the problem is.
      placeholder: E.g., I find it hard to track my daily hydration volume totals...
  - type: textarea
    id: solution
    attributes:
      label: Describe the Solution You'd Like
      description: A clear and concise description of what you want to happen.
      placeholder: Add a wellness dashboard or metrics graph in the settings window.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Describe Alternatives You've Considered
      description: A clear and concise description of any alternative solutions or features you've considered.
      placeholder: E.g., Logging it in a separate spreadsheet manually.
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context, screenshots, or drawings about the feature request here.
