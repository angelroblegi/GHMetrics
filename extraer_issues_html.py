  const cachedToken = this.cache.get();
    if (cachedToken) {
      return cachedToken;
    }
    if (this.isTokenPromise) {
Expected non-Promise value in a boolean conditional.
      return this.isTokenPromise;
    }
    this.isTokenPromise = this.fetchTokenWithRetry();
    try {
      return await this.isTokenPromise;
    } finally {
      this.isTokenPromise = null;
    }
