FROM node:22-bookworm-slim AS build
WORKDIR /app
COPY backend/package*.json ./backend/
RUN cd backend && npm ci
COPY backend ./backend
RUN cd backend && npx prisma generate && npm run build

FROM node:22-bookworm-slim
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/backend/package*.json ./backend/
COPY --from=build /app/backend/node_modules ./backend/node_modules
COPY --from=build /app/backend/dist ./backend/dist
COPY --from=build /app/backend/prisma ./backend/prisma
COPY backend/docker-entrypoint.sh ./backend/docker-entrypoint.sh
COPY data ./data
RUN chmod +x ./backend/docker-entrypoint.sh
WORKDIR /app/backend
EXPOSE 3001
ENTRYPOINT ["./docker-entrypoint.sh"]
