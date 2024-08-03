Section 1: Data Source Understanding
Question 1: Explain the differences between Facebook Ads, Google Ads, RDS (Relational Database Service), and CleverTap in terms of data structure, API access, and data types.

## Differences Between Facebook Ads, Google Ads, RDS, and CleverTap

### Facebook Ads
A platform for managing and optimizing advertising campaigns across Facebook's ecosystem.

#### Data Structure:
*	Hierarchy: Facebook Ads organizes data into Campaigns, Ad Sets, and Ads. At the top, Campaigns set the overall strategy and budget. Ad Sets are nested within Campaigns and define targeting options and schedules. Ads, the lowest level, are the actual creatives displayed to users.
8	Purpose: This setup allows for detailed management and optimization of advertising efforts, making it easier to track performance at various levels.

#### API Access:
*	API: Managed through the Facebook Marketing API, a subset of the Graph API.
*	Authentication: Uses OAuth 2.0, ensuring secure access to your data.
*	Endpoints: here are some of the most used endpoints:
  *	/act_{ad_account_id}/ads: For ad management.
  *	/act_{ad_account_id}/adsets: For ad set management.
  *	/act_{ad_account_id}/campaigns: For campaign management.
* Rate Limits: Rate limits are in place to manage usage and prevent excessive load, with batch requests helping to optimize performance.

#### Data Types:
*	Metrics: Includes data like impressions, clicks, conversions, and spend.
*	Attributes: Details such as ad name, ID, campaign ID, targeting details, and creative content.
*	Format: Data is returned in JSON format, making it easy to parse and integrate.

### Google Ads
A service for creating and managing online ads that appear in Google search results and across its advertising network.

#### Data Structure:
*	Hierarchy: Google Ads also follows a hierarchical structure with Campaigns, Ad Groups, and Ads. Campaigns set the overall goal and budget, Ad Groups contain ads and keywords for specific targeting, and Ads are the actual content seen by users.
*	Purpose: This structure helps in precise management and optimization of ad campaigns.

#### API Access:
*	API: Accessed through the Google Ads API.
*	Authentication: OAuth 2.0 is used for secure API access.
*	Endpoints: Key endpoints include:
  -	customers/{customerId}/googleAds:search: For retrieving ad performance data.
  -	Additional endpoints for managing other elements like campaigns and ad groups.
*	Rate Limits: Imposes rate limits to ensure fair and efficient use of the API.

#### Data Types:
*	Metrics: Clicks, impressions, cost, and conversions.
*	Attributes: Includes ad name, ad group ID, campaign ID, keyword performance, and targeting settings.
*	Format: Data is provided in JSON format.

### RDS (Relational Database Service)
A managed AWS database service that simplifies the setup, operation, and scaling of relational databases in the cloud.

#### Data Structure:
*	Schema-Based: RDS uses a relational database model where data is organized into tables with rows and columns, following a predefined schema.
*	Purpose: This setup supports structured data and complex queries, making it suitable for transactional and analytical purposes.

#### API Access:
*	API: Managed through AWS SDKs and standard database access methods like JDBC/ODBC.
*	Endpoints:
  -	AWS SDKs: For programmatic access.
  -	JDBC/ODBC: For standard database connectivity.
*	Authentication: Uses IAM roles and database credentials for secure access.

#### Data Types:
*	Structured Data Types: Includes integers, strings, dates, and timestamps.
*	Complex Data Types: Supports additional formats like JSON and XML for flexibility.

### CleverTap
A customer engagement and analytics platform for tracking user behavior and personalizing marketing strategies.

#### Data Structure:
*	Event-Driven: CleverTap is built around event-based data and user profiles. Events track user actions (like app opens or purchases), while user profiles store detailed demographic and behavioral information.
*	Purpose: This flexible structure allows for in-depth analysis of user behavior and engagement.

#### API Access:
*	API: CleverTap REST API.
*	Authentication: Secured using account-specific tokens.
*	Endpoints:
  -	/events: For recording and querying event data.
  -	/profiles: For managing user profiles.
*	Rate Limits: Rate limits help manage usage and maintain performance.

#### Data Types:
*	Event Data: Includes event names, timestamps, and properties.
*	User Profile Data: Attributes such as user name, email, and device information.
*	Format: Data is returned in JSON format.
