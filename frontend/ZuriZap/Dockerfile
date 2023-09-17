FROM node
WORKDIR /app
COPY package.json .
RUN npm install
RUN npm install @material-tailwind/react
COPY . .
## EXPOSE [Port you mentioned in the vite.config file]
EXPOSE 8080
CMD ["npm", "run", "dev-docker"]