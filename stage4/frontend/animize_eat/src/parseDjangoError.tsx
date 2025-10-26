const parseDjangoError = async (response: Response): Promise<string> => {
  try {
    const data = await response.json();
    // If error is string
    if (typeof data === 'string') return data;
    // If error is an object with 'detail' or 'error'
    if (data.detail) return data.detail;
    if (data.error) return data.error;
    // If error is a dict of field errors (e.g., {username: ["This field is required."]})
    if (typeof data === 'object') {
      return Object.entries(data)
        .map(([field, messages]) =>
          Array.isArray(messages)
            ? `${field}: ${messages.join(', ')}`
            : `${field}: ${messages}`
        )
        .join('\n');
    }
    // Fallback
    return 'Unknown error';
  } catch {
    return 'Unknown error';
  }
};

export default parseDjangoError;
