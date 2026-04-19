# Tinder AppTweak Analytics

## Problem Statement

1. Competitive Landscape

The global dating app market has become increasingly saturated, with strong regional competitors and niche platform
eroding Tinder’s market share in key geographies. Competitors differentiate through features such as algorithmic
matching, community focus, or cultural positioning, making it harder for Tinder to maintain user acquisition efficiency
and engagement. Without a clear, data-driven understanding of competitive positioning by market and category, Tinder risks
declining visibility, lower install growth, and reduced user retention.

2. Localization

Tinder’s current product, marketing, and App Store presence are not sufficiently localized to meet the cultural, linguistic,
and behavioral expectations of users across diverse markets. As a result, conversion rates, engagement, and retention vary
significantly by country. Without deeper localization of features, messaging, and keyword strategy, Tinder risks
underperforming in high-growth international markets and losing ground to locally optimized competitors.

In this project I address both of these issues using AppTweak metrics to better understand the competitive landscape and
localization issues and provide insights into business strategies to drive growth.

## Analytics Workflow

![Analytics Workflow](images/workflow.png)

1. Data ingestion

Data is extracted from the AppTweak API using scheduled Python scripts. These scripts run on a fixed cadence
(depends on data freshness requirements) via a cloud scheduler. The API responses are cleaned, validated,
and lightly transformed (e.g. formatting, deduplication, and basic quality checks) before being loaded
into the cloud data warehouse.

2. Transformation / Analysis

Once data is loaded, dbt is used to perform structured transformations inside the warehouse. This includes
building staging models for raw API data, intermediate aggregation layers, and final fact tables. Key metrics
include keyword and category rankings, visibility scores, and country/category-level performance trends, which are
standardized and made consistent across time and markets.

3. Output

The final transformed tables are exposed to a BI tool, where stakeholders can access dashboards showing
performance trends, competitive positioning, and localization insights. These dashboards support both
strategic analysis and operational monitoring.

4. Automation

The entire pipeline is automated using scheduled jobs. Python ingestion runs on a recurring schedule,
followed by dbt transformations triggered after data load completion. This ensures that dashboards are
continuously updated without manual intervention.

## Analytic Outputs

1. [Competitive Landscape](https://datastudio.google.com/s/kTUdLrQ0nMw)

![Data Studio Dashboard](images/competitive_landscape.png)



