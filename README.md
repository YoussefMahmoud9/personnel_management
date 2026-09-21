### Personnel Management

Personnel management System.

### Complete Documentation

The full professional documentation set is in [`docs/`](docs/README.md).

Recommended starting points:

- [Complete System Guide](docs/COMPLETE_SYSTEM_GUIDE.md)
- [Beginner To Expert Guide](docs/BEGINNER_TO_EXPERT_GUIDE.md)
- [User Guide](docs/USER_GUIDE.md)
- [Administrator Guide](docs/ADMIN_GUIDE.md)
- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)
- [DocType And Field Reference](docs/DOCTYPE_AND_FIELD_REFERENCE.md)
- [Import Export Detailed Guide](docs/IMPORT_EXPORT_DETAILED_GUIDE.md)
- [Conflict And Deduplication Reference](docs/CONFLICT_AND_DEDUPLICATION_REFERENCE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Dashboards, Reports, And Statistics](docs/DASHBOARDS_REPORTS_AND_STATISTICS.md)

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app personnel_management
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/personnel_management
pre-commit install
```

### License

mit
