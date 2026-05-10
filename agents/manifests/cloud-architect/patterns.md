# Cloud Architect — Patterns

### Terraform structure
```
terraform/
├── modules/     → reusable components
├── envs/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── backend.tf   → remote state (S3 + DynamoDB)
```

### Naming convention
```
{project}-{env}-{resource}-{region}
crypto-tracker-prod-ec2-useast1
```

### Security groups
- Mínimo privilegio: solo puertos necesarios
- Nunca 0.0.0.0/0 para SSH
- Bastion host o VPN para acceso admin
