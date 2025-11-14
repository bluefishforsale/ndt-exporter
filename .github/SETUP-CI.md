# GitHub CI Setup for DockerHub

This guide walks through setting up GitHub Actions to automatically build and push Docker images to DockerHub.

## 1. DockerHub Setup

### Create DockerHub Access Token
1. Log in to [DockerHub](https://hub.docker.com)
2. Go to **Account Settings** → **Security** → **Access Tokens**
3. Click **New Access Token**
4. Name: `github-ci-ndt-exporter`
5. Permissions: **Read, Write, Delete**
6. Copy the generated token (you'll only see it once)

## 2. GitHub Repository Secrets

### Add Required Secrets
Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these repository secrets:

| Name | Value | Description |
|------|-------|-------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username | Used for docker login |
| `DOCKERHUB_TOKEN` | Generated access token | Used for docker login authentication |

### Steps to Add Secrets:
1. Click **New repository secret**
2. Enter the name exactly as shown above
3. Paste the corresponding value
4. Click **Add secret**
5. Repeat for both secrets

## 3. Workflow Behavior

### Automatic Builds Trigger On:
- **Push to main/master**: Builds and pushes with `latest` tag
- **Git tags (v*)**: Builds and pushes with semantic version tags
- **Pull requests**: Builds only (doesn't push to DockerHub)

### Image Tags Generated:
- `latest` - Latest main branch build
- `v1.2.3` - Exact version from git tag
- `v1.2` - Major.minor from git tag  
- `v1` - Major version from git tag
- `main` - Branch name
- `pr-123` - Pull request number

### Multi-Platform Support:
- Builds for both `linux/amd64` and `linux/arm64`
- Uses Docker buildx for cross-platform builds
- Optimized with GitHub Actions cache

## 4. Testing the Setup

### Test with a Push:
```bash
# Make a small change
echo "# CI Test" >> README.md
git add README.md
git commit -m "test: trigger CI build"
git push origin main
```

### Monitor the Build:
1. Go to your repository → **Actions** tab
2. Click on the running workflow
3. Monitor the build progress
4. Check DockerHub for the pushed image

### Test with a Release:
```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0
```

This will create multiple tagged images on DockerHub.

## 5. Verification

After successful setup, verify:

- [ ] GitHub Actions workflow runs without errors
- [ ] Images appear in DockerHub repository
- [ ] Both AMD64 and ARM64 architectures are built
- [ ] Pull requests build but don't push
- [ ] Main branch pushes create `latest` tag
- [ ] Git tags create versioned releases

## Troubleshooting

### Common Issues:
- **Authentication failed**: Check DOCKERHUB_USERNAME and DOCKERHUB_TOKEN secrets
- **Permission denied**: Ensure DockerHub token has Write permissions
- **Image not found**: Verify IMAGE_NAME in workflow matches DockerHub repo
- **Build fails**: Check Dockerfile syntax and dependencies

### Debug Steps:
1. Check Actions logs for detailed error messages
2. Verify DockerHub credentials by logging in manually
3. Test local build: `docker buildx build --platform linux/amd64,linux/arm64 .`
4. Ensure repository secrets are correctly named (case-sensitive)
