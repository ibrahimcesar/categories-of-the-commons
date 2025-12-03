#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { InteractiveStack } from '../lib/interactive-stack';

const app = new cdk.App();

new InteractiveStack(app, 'CommonsInteractiveStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
  },
  description: 'Categories of the Commons - Interactive Explorer Platform',
});
