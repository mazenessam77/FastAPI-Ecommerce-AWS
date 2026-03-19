"""
Zero-Touch CI/CD Pipeline Diagram
Remote Build Strategy — No Local Docker Required
FastAPI → GitHub Actions → ECR → Lambda
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.compute import ECR
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.vcs import Github
from diagrams.onprem.client import User
from diagrams.onprem.ci import GithubActions
from diagrams.programming.framework import Fastapi
from diagrams.generic.device import Mobile

graph_attr = {
    "fontsize": "20",
    "fontname": "Helvetica Bold",
    "bgcolor": "#FAFBFC",
    "pad": "1.0",
    "nodesep": "1.0",
    "ranksep": "1.6",
    "splines": "curved",
    "dpi": "200",
    "labelloc": "t",
    "labeljust": "c",
}

with Diagram(
    "",
    filename="/Users/macbookair/Desktop/FastAPI-Ecommerce-API/cicd_zero_touch_pipeline",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    edge_attr={"fontsize": "10", "fontname": "Helvetica", "fontcolor": "#333333"},
    node_attr={"fontsize": "11", "fontname": "Helvetica"},
    outformat="png",
):

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 1: SOURCE — Local Development
    # ══════════════════════════════════════════════════════════════════════
    with Cluster(
        "① SOURCE\nLocal Development",
        graph_attr={
            "style": "rounded",
            "bgcolor": "#E3F2FD",
            "fontsize": "13",
            "fontcolor": "#0D47A1",
            "pencolor": "#1565C0",
            "penwidth": "2",
            "margin": "20",
        },
    ):
        dev = User("Developer\nWorkstation")
        fastapi = Fastapi("FastAPI +\nMangum Code")

    # ══════════════════════════════════════════════════════════════════════
    # SOURCE CONTROL — GitHub Repository
    # ══════════════════════════════════════════════════════════════════════
    with Cluster(
        "Source Control",
        graph_attr={
            "style": "rounded",
            "bgcolor": "#F3E5F5",
            "fontsize": "13",
            "fontcolor": "#4A148C",
            "pencolor": "#7B1FA2",
            "penwidth": "2",
            "margin": "16",
        },
    ):
        github = Github("GitHub Repo\n(main branch)")

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 2: BUILD — GitHub Actions CI/CD
    # ══════════════════════════════════════════════════════════════════════
    with Cluster(
        "② BUILD\nGitHub Actions (Cloud Runner)",
        graph_attr={
            "style": "rounded",
            "bgcolor": "#FFF3E0",
            "fontsize": "13",
            "fontcolor": "#BF360C",
            "pencolor": "#E65100",
            "penwidth": "2",
            "margin": "20",
        },
    ):
        runner = GithubActions("Step 1:\nProvision\nCloud Runner")
        docker_build = GithubActions("Step 2:\nRemote\nDocker Build")
        oidc = IAM("Step 3:\nOIDC Auth\n(Passwordless)")

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 3: SHIP — Amazon ECR
    # ══════════════════════════════════════════════════════════════════════
    with Cluster(
        "③ SHIP\nContainer Registry",
        graph_attr={
            "style": "rounded",
            "bgcolor": "#E8F5E9",
            "fontsize": "13",
            "fontcolor": "#1B5E20",
            "pencolor": "#2E7D32",
            "penwidth": "2",
            "margin": "20",
        },
    ):
        ecr = ECR("Amazon ECR\n(Private Repo)\nTagged Image")

    # ══════════════════════════════════════════════════════════════════════
    # STAGE 4: DEPLOY — AWS Lambda
    # ══════════════════════════════════════════════════════════════════════
    with Cluster(
        "④ DEPLOY\nServerless Compute",
        graph_attr={
            "style": "rounded",
            "bgcolor": "#FFEBEE",
            "fontsize": "13",
            "fontcolor": "#B71C1C",
            "pencolor": "#C62828",
            "penwidth": "2",
            "margin": "20",
        },
    ):
        lam = Lambda("AWS Lambda\n(Production)\nZero-Downtime\nHot Swap")
        cw = Cloudwatch("CloudWatch\nLogs & Metrics")

    # ══════════════════════════════════════════════════════════════════════
    # FLOW EDGES
    # ══════════════════════════════════════════════════════════════════════

    # Source stage
    dev >> Edge(
        label="Code Edit",
        color="#0D47A1",
        style="bold",
    ) >> fastapi

    fastapi >> Edge(
        label="git push origin main",
        color="#7B1FA2",
        style="bold",
    ) >> github

    # Trigger build
    github >> Edge(
        label="Webhook\nTrigger",
        color="#E65100",
        style="bold",
    ) >> runner

    # Build pipeline (sequential steps)
    runner >> Edge(
        label="docker build\n--platform linux/arm64",
        color="#E65100",
        style="bold",
    ) >> docker_build

    docker_build >> Edge(
        label="Assume Role\nvia OIDC",
        color="#E65100",
        style="bold",
    ) >> oidc

    # Ship to ECR
    oidc >> Edge(
        label="docker push\n(Tagged Image)",
        color="#2E7D32",
        style="bold",
    ) >> ecr

    # Deploy to Lambda
    ecr >> Edge(
        label="UpdateFunctionCode\n(Image Digest)",
        color="#C62828",
        style="bold",
    ) >> lam

    # Observability
    lam >> Edge(
        label="Logs",
        color="#F57F17",
        style="dotted",
    ) >> cw


print("Pipeline diagram generated!")
print("→ /Users/macbookair/Desktop/FastAPI-Ecommerce-API/cicd_zero_touch_pipeline.png")
