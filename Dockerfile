FROM node:20-alpine AS builder

WORKDIR /app

# Copie les fichiers de dépendances
COPY package.json pnpm-lock.yaml* ./

# Installe pnpm si besoin
RUN npm install -g pnpm

# Installe les dépendances
RUN pnpm install --frozen-lockfile

# Copie le reste du code source
COPY . .

# Désactive le lint Next.js pendant le build
ENV NEXTJS_DISABLE_ESLINT=1

# Build l'app
RUN pnpm build

# --------- Phase de production ---------
FROM node:20-alpine AS runner

WORKDIR /app

# Installe pnpm dans l'image finale
RUN npm install -g pnpm

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/pnpm-lock.yaml ./pnpm-lock.yaml
COPY --from=builder /app/node_modules ./node_modules
# COPY --from=builder /app/next.config.js* ./

ENV NODE_ENV=production

EXPOSE 3000

CMD ["pnpm", "start"]