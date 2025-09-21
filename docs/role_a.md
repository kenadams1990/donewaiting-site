# Agent A Role - Backend Infrastructure & API Development

Since the UI/UX implementation has been completed, Agent A will focus on backend infrastructure, API development, and deployment configuration tasks that are essential for the Done Waiting petition site.

## Primary Responsibilities

### 1. Cloudflare Worker API Implementation
- **Task**: Create `src/worker.mjs` - Cloudflare Worker for petition API endpoints
- **Endpoints to implement**:
  - `/api/sign` - Handle petition signatures with validation
  - `/api/count` - Return current signature count
  - `/api/count?group=state` - Return signatures grouped by state
  - `/api/count?state={STATE_CODE}` - Return signature count for specific state
- **Requirements**:
  - Integrate Cloudflare Turnstile for bot protection
  - Handle CORS properly for allowed origins
  - Store signatures securely (use Cloudflare D1 or KV storage)
  - Implement proper error handling and response codes
  - Support redirect parameter for thank-you page routing

### 2. Worker Configuration
- **Task**: Create `wrangler.toml` configuration file
- **Requirements**:
  - Configure environment variables (non-secret ones)
  - Set up proper routing and domain bindings
  - Configure compatibility settings
  - Set up KV namespace or D1 database bindings for signature storage

### 3. Netlify Deployment Configuration
- **Task**: Create `netlify.toml` configuration file
- **Requirements**:
  - Configure build settings and publish directory
  - Set up redirects and headers properly
  - Configure environment variables for the static site
  - Set up proper caching headers for static assets

### 4. Environment and Security Setup
- **Task**: Document and configure environment variables and secrets
- **Requirements**:
  - Document all required environment variables
  - Create templates for secret configuration
  - Ensure TURNSTILE_SITEKEY is properly configured
  - Set up secure secret management practices

### 5. API Integration Testing
- **Task**: Test and validate API endpoints work with the existing frontend
- **Requirements**:
  - Verify the petition form in `index.html` works with new API
  - Test signature counting functionality
  - Validate thank-you page redirection works properly
  - Test error handling and edge cases

### 6. Performance and Monitoring
- **Task**: Implement basic monitoring and performance optimization
- **Requirements**:
  - Add basic logging for API requests
  - Implement rate limiting to prevent abuse
  - Optimize API response times
  - Set up basic error tracking

## Technical Specifications

### API Endpoints Detail

#### POST /api/sign
- **Purpose**: Accept and store petition signatures
- **Required fields**: name, email, city, state
- **Optional fields**: role, message
- **Validation**: 
  - Email format validation
  - State code validation (US states + DC)
  - Turnstile verification
- **Response**: Redirect to thank-you page or JSON response

#### GET /api/count
- **Purpose**: Return current signature count
- **Parameters**: 
  - `group=state` (optional): Return signatures grouped by state
  - `state={STATE_CODE}` (optional): Return count for specific state
- **Response**: JSON with signature count or state breakdown
- **Caching**: Implement appropriate caching headers

### Security Requirements
- Implement Turnstile bot protection on form submission
- Validate all input data server-side
- Use HTTPS only
- Implement proper CORS headers
- Rate limiting on API endpoints

### Data Storage
- Store signatures with: name, email, city, state, role, message, timestamp
- Implement data retention policies
- Ensure GDPR/privacy compliance considerations
- Do not store sensitive payment or authentication data

## Success Criteria
- [ ] Cloudflare Worker API fully functional
- [ ] Petition form successfully submits signatures
- [ ] Signature counter displays real-time counts
- [ ] Thank-you page redirection works
- [ ] All configurations are properly documented
- [ ] API handles error cases gracefully
- [ ] Performance meets requirements (< 200ms response time)

## Notes
- The frontend UI/UX work has been completed by another agent
- Focus on backend functionality and infrastructure
- Coordinate with agents B and C on their respective tasks
- Maintain compatibility with existing frontend implementation
- Follow security best practices for handling user data