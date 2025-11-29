#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { GitHubCollectorStack } from "../lib/github-collector-stack";

const app = new cdk.App();

new GitHubCollectorStack(app, "GitHubCollectorStack", {
  description: "GitHub data collection infrastructure for Categories of the Commons",
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || "us-east-1",
  },
  tags: {
    Project: "categories-of-the-commons",
    Environment: "production",
  },
});
