# Use the official Node.js image as the base image
FROM node:18-alpine

# Set the working directory to the project root (where package.json is)
WORKDIR /app

# Copy the package.json and lock file to the container
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the Next.js application for production
RUN npm run build

# Expose the default Next.js port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "start"]
