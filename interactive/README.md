# Categories of the Commons - Interactive Explorer

An interactive React application for exploring OSS governance patterns and contributing to the research dataset.

## Features

- **Explore Dataset**: Browse and visualize collected governance metrics
- **Interactive Equations**: Understand entropy calculations with live examples
- **Compare Projects**: See how different projects compare across categories
- **Contribute Data**: Add your own GitHub repos to the dataset

---

## Quick Start (Local Development)

### Prerequisites

- Node.js 18+ and npm
- (Optional) Python 3.9+ for Lambda functions

### 1. Install Dependencies

```bash
cd interactive
npm install
```

### 2. Download Dataset

The application uses a pre-built gzipped dataset. Download it before running:

```bash
# Option A: Using npm script
npm run download-data

# Option B: Manual download
curl -L -o dataset.tar.gz \
  https://github.com/ibrahimcesar/categories-of-the-commons/releases/latest/download/dataset.tar.gz
tar -xzf dataset.tar.gz -C public/
rm dataset.tar.gz
```

The extracted dataset structure:

```
public/data/
├── summary.json           # Dataset overview and category stats
├── projects/              # Individual project metrics (91 files)
│   ├── kubernetes_kubernetes.json
│   ├── curl_curl.json
│   └── ...
└── categories/            # Aggregated category data
    ├── federation.json
    ├── stadium.json
    ├── club.json
    └── toy.json
```

### 3. Start Development Server

```bash
npm run dev

# Open http://localhost:3000
```

### Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (port 3000) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint |
| `npm run download-data` | Download latest dataset |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CloudFront CDN                                │
│                    (https://commons.your-domain.com)                 │
└─────────────────────────────────────────────────────────────────────┘
                    │                           │
          Static Assets                    /api/* routes
                    │                           │
                    ▼                           ▼
            ┌──────────────┐           ┌──────────────────┐
            │  S3 Bucket   │           │   API Gateway    │
            │  (Website)   │           │                  │
            └──────────────┘           └──────────────────┘
                                                │
                                    ┌───────────┴───────────┐
                                    ▼                       ▼
                            ┌──────────────┐       ┌──────────────┐
                            │   Lambda     │       │   Lambda     │
                            │  (Dataset)   │       │ (Contribute) │
                            └──────────────┘       └──────────────┘
                                    │                       │
                                    ▼                       ▼
                            ┌──────────────┐       ┌──────────────┐
                            │  S3 (Data)   │       │  DynamoDB    │
                            └──────────────┘       └──────────────┘
```

---

## AWS Deployment

### 1. Deploy Infrastructure (CDK)

```bash
cd interactive/infra
npm install

# Bootstrap CDK (first time only)
cdk bootstrap aws://ACCOUNT_ID/us-east-1

# Deploy stack
cdk deploy
```

### 2. Deploy Frontend

```bash
cd interactive
npm run build

# Upload to S3
aws s3 sync dist/ s3://commons-interactive-ACCOUNT_ID --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id DISTRIBUTION_ID \
  --paths "/*"
```

### 3. Upload Dataset

```bash
aws s3 sync ../data/raw/ s3://commons-interactive-data-ACCOUNT_ID/raw/
```

---

## Rate Limiting

| Limit | Value | Reason |
|-------|-------|--------|
| Per repo | 1x/day | Avoid excessive API calls |
| Per user | 10/day | Fair usage |
| Global | 100/day | API budget |

---

## Project Structure

```
interactive/
├── src/
│   ├── components/          # UI components (GitHub dark theme)
│   ├── pages/               # Route pages
│   │   ├── HomePage.tsx
│   │   ├── ExplorePage.tsx
│   │   ├── EquationsPage.tsx
│   │   ├── ComparePage.tsx
│   │   ├── ContributePage.tsx
│   │   └── ProjectPage.tsx
│   └── types/
├── public/data/             # Downloaded dataset
├── lambda/                  # AWS Lambda functions
└── infra/                   # AWS CDK infrastructure
```

---

## Environment Variables

```env
VITE_API_URL=https://api.example.com
VITE_DATA_PATH=/data
```

---

## License

Part of the Categories of the Commons research project.
