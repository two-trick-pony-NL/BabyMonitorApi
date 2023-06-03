import { CfnOutput, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as ddb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class babyMonitorApi extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create DDB table to store the tasks.
    const table = new ddb.Table(this, "Measurements", {
      partitionKey: { name: "measurementId", type: ddb.AttributeType.STRING },
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
    });

    // Add GSI based on user_id.
    table.addGlobalSecondaryIndex({
      indexName: "user-index",
      partitionKey: { name: "userId", type: ddb.AttributeType.STRING },
      sortKey: { name: "lastUpdate", type: ddb.AttributeType.NUMBER },
    });

    // Create Lambda function for the API.
    const api = new lambda.Function(this, "API", {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset("../api/lambda_function.zip"),
      handler: "crud.handler",
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    // Create a URL so we can access the function.
    const functionUrl = api.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedOrigins: ["*"],
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ["*"],
      },
    });

    // Output the API function url.
    new CfnOutput(this, "APIUrl", {
      value: functionUrl.url,
    });

    table.grantReadWriteData(api);
  }
}
