"""
AWS Serverless E-Commerce Architecture Diagram
FastAPI Microservices with Mangum on AWS Lambda (Container Images)
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, ECR
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.security import SecretsManager, IAM
from diagrams.aws.integration import SQS
from diagrams.aws.engagement import SES
from diagrams.aws.management import Cloudwatch
from diagrams.aws.devtools import Codepipeline
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github
from diagrams.generic.device import Mobile

with Diagram(
    "AWS Serverless E-Commerce Architecture\nFastAPI Microservices on Lambda (Container Images)",
    filename="/Users/macbookair/Desktop/FastAPI-Ecommerce-API/aws_ecommerce_architecture",
    show=False,
    direction="TB",
    outformat="png",
    graph_attr={
        "fontsize": "22",
        "fontname": "Helvetica Bold",
        "bgcolor": "#FAFBFC",
        "pad": "1.0",
        "nodesep": "0.6",
        "ranksep": "1.2",
        "splines": "polyline",
        "dpi": "150",
    },
    edge_attr={"fontsize": "9", "fontname": "Helvetica"},
    node_attr={"fontsize": "10", "fontname": "Helvetica", "width": "1.5"},
):

    # ── CLIENTS ──
    with Cluster("① Clients (Public Internet)", graph_attr={
        "style": "rounded", "bgcolor": "#E3F2FD",
        "fontsize": "13", "fontcolor": "#0D47A1", "pencolor": "#1565C0", "penwidth": "2"
    }):
        web = Users("Web\nBrowser")
        mob = Mobile("Mobile\nApp")

    # ── CDN / STATIC ──
    with Cluster("② Edge / CDN", graph_attr={
        "style": "rounded", "bgcolor": "#E8EAF6",
        "fontsize": "13", "fontcolor": "#283593", "pencolor": "#3949AB", "penwidth": "2"
    }):
        cf = CloudFront("CloudFront")
        s3 = S3("S3 Static\nAssets")

    # ── API GATEWAY ──
    with Cluster("③ API & Auth", graph_attr={
        "style": "rounded", "bgcolor": "#FFF3E0",
        "fontsize": "13", "fontcolor": "#BF360C", "pencolor": "#E65100", "penwidth": "2"
    }):
        gw = APIGateway("API\nGateway")
        auth = Lambda("JWT\nAuthorizer")

    # ── VPC ──
    with Cluster("VPC  10.0.0.0/16", graph_attr={
        "style": "bold,rounded", "bgcolor": "#E8F5E9",
        "fontsize": "15", "fontcolor": "#1B5E20", "pencolor": "#2E7D32", "penwidth": "3"
    }):

        # Public subnet — Lambdas
        with Cluster("④ Public Subnet — Serverless Microservices (FastAPI + Mangum)", graph_attr={
            "style": "dashed,rounded", "bgcolor": "#C8E6C9",
            "fontsize": "11", "fontcolor": "#2E7D32", "pencolor": "#43A047"
        }):
            la = Lambda("Auth\n/auth")
            lu = Lambda("Users\n/users")
            lp = Lambda("Products\n/products")
            lc = Lambda("Categories\n/categories")
            lk = Lambda("Cart\n/carts")

        # Private subnet — Data
        with Cluster("⑤ Private Subnet — Data & Security", graph_attr={
            "style": "dashed,rounded", "bgcolor": "#A5D6A7",
            "fontsize": "11", "fontcolor": "#1B5E20", "pencolor": "#2E7D32"
        }):
            db = RDS("RDS\nPostgreSQL")
            sm = SecretsManager("Secrets\nManager")

    # ── ASYNC ──
    with Cluster("⑥ Async Processing", graph_attr={
        "style": "rounded", "bgcolor": "#F3E5F5",
        "fontsize": "13", "fontcolor": "#4A148C", "pencolor": "#7B1FA2", "penwidth": "2"
    }):
        sq = SQS("SQS\nOrder Queue")
        wk = Lambda("Worker\nLambda")
        em = SES("SES\nEmail")

    # ── OBSERVABILITY ──
    cw = Cloudwatch("CloudWatch\nLogs / Metrics / Alarms")

    # ── CI/CD ──
    with Cluster("⑦ CI/CD Deployment Pipeline", graph_attr={
        "style": "rounded", "bgcolor": "#ECEFF1",
        "fontsize": "13", "fontcolor": "#263238", "pencolor": "#546E7A", "penwidth": "2"
    }):
        gh = Github("GitHub")
        ci = Codepipeline("GitHub\nActions")
        er = ECR("ECR\nDocker")
        tf = IAM("Terraform\nIaC")

    # ─── EDGES ───────────────────────────────

    # Client -> CDN
    web >> Edge(color="#1565C0") >> cf
    mob >> Edge(color="#1565C0") >> cf
    cf >> Edge(label="images", color="#43A047") >> s3

    # Client -> API GW
    web >> Edge(label="REST", color="#E65100", style="bold") >> gw
    mob >> Edge(label="REST", color="#E65100", style="bold") >> gw
    gw >> Edge(label="validate", color="#C62828", style="dashed") >> auth

    # API GW -> Lambdas
    gw >> Edge(label="/auth", color="#FF8F00") >> la
    gw >> Edge(label="/users", color="#FF8F00") >> lu
    gw >> Edge(label="/products", color="#FF8F00") >> lp
    gw >> Edge(label="/categories", color="#FF8F00") >> lc
    gw >> Edge(label="/carts", color="#FF8F00") >> lk

    # Lambdas -> DB
    la >> Edge(color="#2E7D32") >> db
    lu >> Edge(color="#2E7D32") >> db
    lp >> Edge(color="#2E7D32") >> db
    lc >> Edge(color="#2E7D32") >> db
    lk >> Edge(color="#2E7D32") >> db

    # Secrets
    sm >> Edge(color="#7B1FA2", style="dashed") >> la
    sm >> Edge(color="#7B1FA2", style="dashed") >> lp
    sm >> Edge(color="#7B1FA2", style="dashed") >> lk

    # Async
    lk >> Edge(label="order event", color="#7B1FA2", style="bold") >> sq
    sq >> Edge(color="#7B1FA2", style="bold") >> wk
    wk >> Edge(label="send email", color="#7B1FA2", style="bold") >> em

    # Observability (minimal to reduce clutter)
    gw >> Edge(color="#FBC02D", style="dotted") >> cw
    lp >> Edge(color="#FBC02D", style="dotted") >> cw
    db >> Edge(color="#FBC02D", style="dotted") >> cw
    wk >> Edge(color="#FBC02D", style="dotted") >> cw

    # CI/CD
    gh >> Edge(label="push", color="#455A64", style="bold") >> ci
    ci >> Edge(label="build docker", color="#455A64", style="bold") >> er
    ci >> Edge(label="terraform", color="#455A64") >> tf
    er >> Edge(label="deploy images", color="#E65100", style="bold") >> lp

print("Done! → aws_ecommerce_architecture.png")
